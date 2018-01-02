

def soft_update_network(target, source, tau):
    for target_param, source_param in zip(target.parameters(), source.parameters()):
        target_param.data.copy_(
            target_param.data * (1 - tau) + source_param.data * tau
        )

def hard_update_network(target, source):
    target.load_state_dict(source.state_dict())