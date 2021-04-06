import nextConnect from "next-connect"
import middleware from "../../middleware/database"

const handler = nextConnect()

handler.use(middleware)

handler.get(async (req, res) => {
  let doc = await req.db.collection("Strategy").find().toArray()
  console.log("strategy폴더의 doc = ", doc)
  res.json(doc)
})

export default handler
