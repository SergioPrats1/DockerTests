The test on this folder creates a Postgres container with a Volume to verify that actions on the database may be 
kept after the container is stopped when we have the volume.

PREREQUISITES

This test runs on Docker Desktop for Windows.

INSTRUCTIONS

- Start Docker CE, open the command prompt and from the Postgres test folder, 
  execute the following command to start the container:
  
  docker-compose up -d

- From another commmand prompt, run some SQL sentences, for example:

  docker exec -it my_postgres psql -U postgres -c "create database my_database"
  docker exec -it my_postgres psql -U postgres -c "CREATE TABLE ABC (ID INT PRIMARY KEY     NOT NULL, NAME           TEXT  ); "
  docker exec -it my_postgres psql -U postgres -c "INSERT INTO ABC (ID, Name) VALUES( 1, 'HI');” 
  docker exec -it my_postgres psql -U postgres -c "SELECT * FROM ABC;”
  
  The last command should return the records inside the table.  

- Stop the container: docker stop my_postgres

- Start the container again: docker start my_postgres.

- Verify that the records are still in the container.


- Extra: to view the created volume you need to navigate to the Linux virtual machine,
  that can be done by starting this container in interactive mode:
  
  docker container run --rm -it -v /:/host alpine
  
  And executing this linux command: chroot /host
  
  Navigate to the docker volume folder and see the files there:
  
  cd var/lib/docker/volumes/postgres_my_dbdata/_data

