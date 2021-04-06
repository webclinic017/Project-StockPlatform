import { MongoClient } from "mongodb"
import nextConnect from "next-connect"

const client = new MongoClient(
  "mongodb+srv://admin:admin@cluster0.kjrlb.mongodb.net/<pnu_sgm_platformdata>?retryWrites=true&w=majority"
)

async function database(req, res, next) {
  if (!client.isConnected()) {
    console.log("unconnected")
    await client.connect()
  }

  req.dbClient = client
  req.db = client.db("pnu_sgm_platformdata")

  return next()
}

const middleware = nextConnect()

middleware.use(database)

export default middleware
