import { Hono } from "@hono";

export class Cluster {
    private id: string;
    private nodes: Array<{ host: string; port: number }> = [];

    constructor(public options: {id: string}) {
        this.id = options.id;
    }

    at(host: string, port: number) {
        const hostname = host
        const app = this.app()
        Deno.serve({ hostname, port }, app.fetch)
        return this
    }

    join(host: string, port: number) {
        this.nodes.push({ host, port });
        return this;
    }


    private app(): Hono {
        const app = new Hono()

        app.get("/", (c) => {
            return c.json({ id: this.id, nodes: this.nodes });
        })

        return app
    }

}