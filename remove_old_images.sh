#!/bin/bash
for id in `docker images | grep '<none>' | awk '{print $3}'`; do
	docker rmi $id
done
