//몽고디비에서 kospi 값 가져옴

import { MongoClient } from 'mongodb';
import nextConnect from 'next-connect';

const client = new MongoClient('mongodb+srv://user1:start3we@cluster0.mqlrz.mongodb.net/pj_sgm?retryWrites=true&w=majority', {
  useNewUrlParser: true,
  useUnifiedTopology: true,
});

async function database(req, res, next) {
  if (!client.isConnected()) await client.connect();
  req.dbClient = client;
  req.db = client.db('pj_sgm');
  return next();
}

const kospimiddleware = nextConnect();

kospimiddleware.use(database);

export default kospimiddleware;