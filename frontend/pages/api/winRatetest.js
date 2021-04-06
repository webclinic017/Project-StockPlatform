import nextConnect from "next-connect"
import middleware from "../../middleware/database"

const handler = nextConnect()

handler.use(middleware)

handler.get(async (req, res) => {
  // console.log("ok")
  var myReferenceToThis = this
  let doc = await req.db
    .collection("Results")
    .find({}, { projection: { Winning_rate: 1, _id: 0 } })
    .toArray()

  res.json(doc)
})
export default handler
