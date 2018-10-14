#!/bin/bash
FUNCTION_NAME=SmartHomeFunction
ARCHIVE_NAME=Archive.zip

rm -f ./$ARCHIVE_NAME
zip -r $ARCHIVE_NAME ./ -x "*.DS_Store" -x "upload.sh"

/Users/Kristina/Library/Python/2.7/bin/aws lambda update-function-code --function-name $FUNCTION_NAME --zip-file "fileb://$ARCHIVE_NAME" --publish --output text
