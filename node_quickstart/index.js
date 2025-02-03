const { MongoClient } = require("mongodb");
// Replace the uri string with your connection string.
const uri = "mongodb+srv://rivajain:1lRzuNwJOmG6USla@hack-violet.uqo9q.mongodb.net/?retryWrites=true&w=majority&appName=hack-violet";
const client = new MongoClient(uri);
async function run() {
  try {
    const database = client.db('AI-data');
    const movies = database.collection('images-and-interpretations');
    // Query for a movie that has the title 'Back to the Future'
    const query = { str_id: "679eb3dcf630cd4042fe3cd4" };
    const movie = await movies.findOne(query);
    console.log(movie);
  } finally {
    
    // Ensures that the client will close when you finish/error
    await client.close();
  }
}
run().catch(console.dir);