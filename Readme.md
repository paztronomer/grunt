## Grunt

Grunt is a Go server and Docker to emulate Sergeant on a small scale.


## Building

make grunt

## Usage

A service consists of the following fields:

```
endPoint      -- REST endpoint, e.g. /rest/service/<endPoint>
commandLine   -- Command line to run
                 Some special command line parameters are
                 @value  -- replace this argument with the parameter from the POST
                 <in     -- look for an uploaded file
                 >out    -- the process will generate this file for later download
description   -- description of the endpoint
defaults      -- a hashmap of default values for "@value" parameters
```

this example configuration file exposes 2 endpoints, test and copy
test simply echos the input and can be called like this:

```
curl -X POST  -v --form Message=hi localhost:9991/rest/service/test
```

copy takes input and output files.  `<in` must be provided

```
curl -X POST  -v --form in=@big_file.txt --form out=small_file.txt localhost:9901/rest/service/copy
```

NB: "--form in=@big_file.txt" indicates that curl should send big_file.txt as the form parameter `in`
and the output filename is set to "small_file.txt"

to retrieve the output data, first find the UUID in the response, and request the file

```
wget localhost:9901/rest/job/eab4ab07-c8f7-44f7-b7d8-87dbd7226ea4/file/out
```

*NB:* we request the output file using the `out` parameter, not the filename we requested

Here is the copy example using jq(http://stedolan.github.io/jq/) to help a bit

```
id=`curl --silent -X POST --form in=@big_file.txt --form out=small_file.txt localhost:9901/rest/service/copy | jq -r .uuid`
wget --content-disposition localhost:9901/rest/job/$id/file/out
```


## Development

These tools are written in the (Go language)[https://golang.org/].

```
make help
```