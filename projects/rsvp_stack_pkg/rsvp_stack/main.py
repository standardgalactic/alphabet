import hydra
from omegaconf import DictConfig
from rsvp_stack.stack import RSVPStack

@hydra.main(version_base=None, config_path="configs", config_name="config")
def main(cfg: DictConfig):
    print(cfg)
    stack = RSVPStack(cfg)
    results = stack.run()
    print("Completed modules:", list(results.keys()))

if __name__ == "__main__":
    main()