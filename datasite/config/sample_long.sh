#/bin/bash
# Assuming this location: /usr/local/bin/sample_long.sh
# Make sure to chmod +x /usr/local/bin/sample_long.sh


while true
do
    # Echo current date to stdout
    echo `date`
    # Echo 'error!' to stderr
    echo 'error!' > &2
    sleep 1
done

