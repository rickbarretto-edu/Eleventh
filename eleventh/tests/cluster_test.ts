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

async function waitAllHaveThree(apis: ReturnType<typeof wsApi>[], timeoutMs = 2000) {
    const deadline = Date.now() + timeoutMs

    async function allHaveThree(): Promise<boolean> {
        for (const api of apis) {
            const p = await api.peers
            if (p.length !== 3) return false
        }
        return true
    }

    while (Date.now() < deadline) {
        if (await allHaveThree()) return
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
        // wait briefly for servers to be ready
        await sleepFor(200)

        const apis = peers.map(p => wsApi(p))

        // Attach every server to every other server to form a full mesh
        for (let i = 0; i < apis.length; i++) {
            for (let j = 0; j < peers.length; j++) {
                if (i === j) continue
                await apis[i].attach(peers[j])
            }
        }

        // wait until all servers report 3 peers or timeout
        await waitAllHaveThree(apis)

        // verify each server sees all three peers
        for (const api of apis) {
            const p = await api.peers
            expect(p.length).toBe(3)

            // ensure every configured peer is present
            for (const expected of peers) {
                const found = p.some(x => x.host === expected.host && x.port === expected.port)
                expect(found).toBe(true)
            }
        }

        // cleanup apis
        for (const api of apis) {
            try { api[Symbol.dispose]?.() } catch (_e) { /* ignore disposal errors */ }
        }
    } finally {
        // stop servers
        controllers.forEach(c => c.abort())
    }
})
