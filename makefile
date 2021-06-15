TAG=builder-mpi

export NNODES=4

build:
	docker build -t $(TAG) .

rebuild:
	docker build --no-cache -t $(TAG) .

start_two:
	docker-compose up -d --scale mpi_head=1 --scale mpi_node=2 --no-recreate
	docker-compose exec --privileged mpi_head mpirun --allow-run-as-root -n 2 python3 /home/mpirun/builder/main.py
	docker-compose down

start_four:
	docker-compose up -d --scale mpi_head=1 --scale mpi_node=${NNODES} --no-recreate
	docker-compose exec --privileged mpi_head mpirun --allow-run-as-root -n ${NNODES} python3 /home/mpirun/builder/main.py
	docker-compose down
