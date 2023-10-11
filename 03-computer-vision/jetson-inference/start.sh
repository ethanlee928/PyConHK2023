docker run -it --rm --network host -v ${PWD}:/app/ -v ${PWD}/networks:/jetson-inference/data/networks -w /app/ jetson-inference:3.8 bash
