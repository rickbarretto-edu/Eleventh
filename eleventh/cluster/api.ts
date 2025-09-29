import { Peer } from "./models.ts"

export interface ClusterApi {
    peers: Peer[]
    attach(peer: Peer): Promise<void>
    disconnect(peer: Peer): Promise<void>
}