#!/bin/bash

caseName=$1
if [[ -z $caseName ]]
 then
  caseName="default"
fi

blockchainName=$2
if [[ -z $blockchainName ]]
 then
  blockchainName="ETH"
fi

fullFunctionName="CreateNFTFunction${blockchainName}"
eventFile="events/${caseName}.json"

echo "Invoke ${fullFunctionName}"
echo "event: ${eventFile}"

sam local invoke $fullFunctionName -e $eventFile --env-vars env.json --profile sharpshark

if [ $? -eq 0 ]; then
    echo "Invoke SUCCESS!"
else
    echo "Invoke FAIL"
fi

