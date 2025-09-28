import { uuid4 } from "./uuid.ts";
import { cmd } from "./cli.ts"
import { Cluster } from "./cluster/mod.ts";


const initCluster = async () => {

    const { options } = await cmd.parse(Deno.args)

    const id = uuid4("Eleventh");
    const cluster = new Cluster({id})
        .at(options.host, options.port)
    
    if (options.joins) {
        const [host, port] = options.joins.split(":")
        cluster.join(host, parseInt(port))
    }

}


if (import.meta.main) {
    initCluster()
}
