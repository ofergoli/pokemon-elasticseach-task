# Net App - Pokemon Search - Ofer Golibroda


#### Summery

I create an application that initial index called netapp with type called pokemon.
The index is mapped with the following mapping:
1. Using standart tokenizer lowercase for autocompelete search.

2. Dynamiclly by the docuemnt fields that added, update the mapping with the new field. In order to handle the case that the object of the pokemon will change in the future.

3. Using Redis in order to cache queried docs for 5 second (as asked) and have a state on the current fields that we need to mapping if we got new fields.

So the project in order to run need elasticsearch and redis
elastic: http://localhost:9200
redis: http://localhost:6379

The endpoint for create a document is:

```
    PUT requset:
    
     http://localhost:5000/api
    
    body example:
        {
           "pokadex_id": 25,
           "name": "Pikachu",
           "nickname": "Baruh Ha Gever",
           "level": 60,
           "type": "ELECTRIC",
           "skills": [
               "Tail Whip",
               "Thunder Shock",
               "Growl",
               "Play Nice",
               "Quick Attack",
               "Electro Ball",
               "Thunder Wave"
           ]
        }
```

The endpoint for query a document is:
```
    GET requset:
    
     http://localhost:5000/api/autocomplete/<term>
    
    body example:
        {
           "pokadex_id": 25,
           "name": "Pikachu",
           "nickname": "Baruh Ha Gever",
           "level": 60,
           "type": "ELECTRIC",
           "skills": [
               "Tail Whip",
               "Thunder Shock",
               "Growl",
               "Play Nice",
               "Quick Attack",
               "Electro Ball",
               "Thunder Wave"
           ]
        }
```

#### Question 3

Because we and to check if requests success and fail as well it would be better to run our code in the loadbalancer we are using for example write lua script that nginx can run, than we can handle backend responses , i mean requests that get into our nginx load balancer forward into the python application for example and go back to nginx in order to complete the request handle.
In that way we can know if we have failures request with status of 400/500 as well

I guess that the solution should handle massive requests logger so a possible option would be using amazon firehose architecture which is a queue that proccess messages and create records in s3.
The bucket that the firehose sending data into will create records by time inside the folders it create automaticlly.

Each request that the server is getting will have authentication for identifer combined with the timestamp of the request in order to be able to query in the future the data easly per user.
and each json that we add into the bucket will hold all the relevent data for example method type,path,status_code etc.

After we have the data in s3 buckets we can use athena (AWS service) in order to run queries over the data we collected.

In order to scale the system we can on demand increase the amount of firehose and the computing we use when quering the data much faster.

License
----

Ofer Golibroda