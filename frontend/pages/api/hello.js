import nextConnect from 'next-connect';
import middleware from '../../middleware/database';

const handler = nextConnect();

handler.use(middleware);

handler.get(async (req, res) => {

    // 특정 필드를 걸려내고 싶을 떄 projection 을 사용한다.
    // Adj Close 는 필요없는 필드인데 중간에 space 가 있어서 그런지 안보여진다.
    // Atlas MongoDB 에 필드 값을 제대로 해서 넣어줘야겠다. (필요없는 부분은 삭제하도록 하자.)
    // MongoDB 에 JSON 파일형식을 shell 에 넣어줬는데 순서대로 들어가지 않았다.
    
    //let doc = await req.db.collection('a005930').find({},{ projection: { _id : 0, High : 0, Low : 0, Open : 0} }).sort({index : 1}).toArray()
    
    
    let doc = await req.db.collection('Users').find().toArray()
    //console.log(doc);
    res.json(doc);
});

export default handler;