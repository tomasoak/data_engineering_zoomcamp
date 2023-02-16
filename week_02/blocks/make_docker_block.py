from prefect.infrastructure.docker import DockerContainer

docker_block = DockerContainer(
    image="tomasoak/prefect:zom",
    image_pull_policy="ALWAYS",
    auto_remove=True
)

docker_block.save("zoom", overwrite=True)