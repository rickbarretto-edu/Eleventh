import { Sync } from "./sync.ts";

// Usage: deno run -A server.ts <id> <host> <port>
const [id, host, portStr] = Deno.args;
const port = Number(portStr);

if (!id || !host || !port) {
  console.error("Usage: deno run -A server.ts <id> <host> <port>")
  Deno.exit(1);
}

const sync = await Sync.new()
const self = { id, host, port }
sync.at(self)
