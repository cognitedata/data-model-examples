#/bin/bash
echo "Running transformations..."
transformations-cli run --external-id tutorial-load-assets
transformations-cli run --external-id tutorial-load-workorders
transformations-cli run --external-id tutorial-load-workitems
transformations-cli run --external-id tutorial-load-asset2children
transformations-cli run --external-id tutorial-load-workorders2assets
transformations-cli run --external-id tutorial-load-workitems2workorders
transformations-cli run --external-id tutorial-load-workitems2assets