import nextConnect from "next-connect"
import resultmiddleware from "../../middleware/database"

const resulthandler = nextConnect()

resulthandler.use(resultmiddleware)

resulthandler.get(async (req, res) => {
  let doc = await req.db
    .collection("Results")
    .find({ strategy_result_id: 4 }, { projection: { _id: 0 } })
    .toArray()
  res.json(doc)
})

export default resulthandler
