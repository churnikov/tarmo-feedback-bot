job "${CI_PROJECT_NAME}-${NOMAD_DC}" {
  datacenters = ["${NOMAD_DC}"]
  type = "service"
  all_at_once = false
  group "${CI_PROJECT_NAME}" {
    count = 1
    task "${CI_PROJECT_NAME}" {
      shutdown_delay = "60s"
      driver = "docker"

      vault {
        policies = ["nomad-server"]
        env = true
      }

      config {
        force_pull = true
        logging {
           type = "json-file"
        }
        labels {
          env = "${NOMAD_DC}"
          app = "${CI_PROJECT_NAME}"
        }
        image = "${DOCKER_REGISTRY_DOMAIN}/${CI_PROJECT_NAME}:${CI_COMMIT_TAG}"
      }
      template {
        data = <<EOH
        RT_HTTPS_PROXY=${RT_HTTPS_PROXY}
        TG_CHAT_ID=${TG_CHAT_ID}
        TG_BOT_TOKEN=${TG_BOT_TOKEN}
        COMMAND_REPLIES_PATH=${COMMAND_REPLIES_PATH}
        EOH
        env  = true
        destination = "version.env"
      }
      resources {
        cpu    = 1000 # MHz
        memory = 1014 # MB
        network {
          port "http_api" { }
        }
      }

      logs {
        max_files     = 3
        max_file_size = 10
      }


      service {
        name = "${CI_PROJECT_NAME}"
        tags = [
            "back",
            "traefik.enable=true",
            "traefik.frontend.entryPoints=http_5000"

        ]

        port = "http_api"
        address_mode = "host"
      }
    }
  }
}
