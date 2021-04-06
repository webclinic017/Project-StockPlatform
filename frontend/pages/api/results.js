import nextConnect from "next-connect"
import middleware from "../../middleware/database"

const handler = nextConnect()

handler.use(middleware)

handler.get(async (req, res) => {
  let doc = await req.db
    .collection("Results")
    // .find({ strategy_result_id: 1 })
    .find()
    .toArray()
  res.json(doc)
})

export default handler
