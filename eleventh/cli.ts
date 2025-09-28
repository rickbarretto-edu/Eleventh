import { Command } from "@cliffy/command"

import { uuid4 } from "./uuid.ts"


export const cmd = new Command()
    .name("Sync DB")
    .version("0.1.0")
    .description("Distributed Eleventh server.")
    .option("-p, --port <number:number>", "Port to run the sync server on.", { default: 4000 })
    .option("--host <string>", "Host to run the sync server on.", { default: "localhost" })
    .option("--joins <string>", "Peer to join on start, in the format host:port", { default: "" })
    .option("--id <string>", "Unique ID for this node.", { default: uuid4("syncdb-") })
