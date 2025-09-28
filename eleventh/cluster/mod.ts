

export class Cluster {
    private id: string;
    private host: string;
    private port: number;
    private nodes: Array<{ host: string; port: number }> = [];

    constructor(public options: {id: string}) {
        this.id = options.id;
        this.host = "localhost";
        this.port = 4000;
    }

    at(host: string, port: number) {
        this.host = host;
        this.port = port;
        return this;
    }

    join(host: string, port: number) {
        this.nodes.push({ host, port });
        return this;
    }

    async listen() {
        console.log(`Listening on ${this.host}:${this.port}`);
        return;
    }

}