import nextConnect from "next-connect"
import middleware from "../../middleware/database"

const handler = nextConnect()

handler.use(middleware)

handler.get(async (req, res) => {
  // console.log("ok")
  var myReferenceToThis = this
  let doc = await req.db //api로 보내는 데이터
    .collection("Results")
    .find({}, { projection: { selected_companys: 1, _id: 0 } })
    .toArray()

  let length = doc.length
  doc = doc[length - 1]
  res.json(doc) //요청하면 주는 데이터
})
export default handler
