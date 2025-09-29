export type Peer = {
    host: string;
    port: number;
}

export type Cluster = {
    name: string
    nodes: Peer[]
}