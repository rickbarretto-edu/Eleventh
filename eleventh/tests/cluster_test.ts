import { expect } from "@std/expect"
import { serve } from "../cluster/server.ts"
import { Peer } from "../cluster/models.ts"
import { newWebSocketRpcSession } from "@capnweb"

function wsApi(peer: Peer) {
    const url = `ws://${peer.host}:${peer.port}/api`
    return newWebSocketRpcSession(url) as unknown as {
        peers: Promise<Peer[]>
        attach(peer: Peer): Promise<void>
        disconnect(peer: Peer): Promise<void>
        // close/dispose symbol may exist
        [Symbol.dispose]?: () => void
    }
}

function sleepFor(ms: number): Promise<void> {
    return new Promise(res => setTimeout(res, ms))
}

async function waitForClusterSetup(apis: ReturnType<typeof wsApi>[], timeoutMs = 2000) {
    const deadline = Date.now() + timeoutMs

    function areAllUp(apis: ReturnType<typeof wsApi>[]): boolean {
        return apis.every(async api => (await api.peers).length === 3)
    }

    while (Date.now() < deadline && !areAllUp(apis)) {
        await sleepFor(50)
    }
}

Deno.test("three servers can join into a cluster mesh", async () => {
    const peers: Peer[] = [
        { host: "127.0.0.1", port: 18081 },
        { host: "127.0.0.1", port: 18082 },
        { host: "127.0.0.1", port: 18083 },
    ]

    // start servers
    const controllers = peers.map(p => serve(p))

    try {
        await sleepFor(200)

        const apis = peers.map(p => wsApi(p))
        await attachMesh(apis, peers);
        await waitForClusterSetup(apis)

        for (const api of apis) {
            const p = await api.peers
            expect(p.length).toBe(3)

            for (const expected of peers) {
                const found = isPresent(expected, p)
                expect(found).toBe(true)
            }
        }

        for (const api of apis) {
            try { api[Symbol.dispose]?.() } catch (_e) { /* ignore */ }
        }
    } finally {
        controllers.forEach(c => c.abort())
    }

    function isPresent(target: Peer, cluster: Peer[]) {
        const samePort = (p: Peer): boolean => p.port === target.port
        const sameHost = (p: Peer): boolean => p.host === target.host
        const samePeer = (p: Peer): boolean => sameHost(p) && samePort(p)

        return cluster.some(p => samePeer(p));
    }
})

async function attachMesh(
    apis: {
        peers: Promise<Peer[]>
        attach(peer: Peer): Promise<void>
        disconnect(peer: Peer): Promise<void> 
        [Symbol.dispose]?: () => void
    }[], 
    peers: Peer[]
) {
    for (let current = 0; current < apis.length; current++) {
        for (let target = 0; target < peers.length; target++) {
            if (current !== target) {
                await apis[current].attach(peers[target]);
            }
        }
    }
}
