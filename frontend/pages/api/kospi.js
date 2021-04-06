import nextConnect from 'next-connect';
import kospimiddleware from '../../middleware/kospidatabase';

const kospihandler = nextConnect();

kospihandler.use(kospimiddleware);

kospihandler.get(async (req, res) => {

    let doc = await req.db.collection('kospi').find({},{projection :{ "kospi.High" : 0, "kospi.Low" : 0, "kospi.Change" : 0, "kospi.Volume" : 0}}).toArray()
    {/*console.log(doc);*/}
    res.json(doc);
    
});

export default kospihandler;