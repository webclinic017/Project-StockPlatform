// import { MongoClient } from "mongodb"
// import nextConnect from "next-connect"

// const client = new MongoClient(
//   "mongodb+srv://admin:admin@cluster0.kjrlb.mongodb.net/test_db_stock?retryWrites=true&w=majority",
//   {
//     useNewUrlParser: true,
//     useUnifiedTopology: true
//   }
// )

// async function database(req, res, next) {
//   if (!client.isConnected()) await client.connect()
//   req.dbClient = client
//   req.db = client.db("test_db_stock")
//   return next()
// }

// const middleware = nextConnect()

// middleware.use(database)

// export default middleware
