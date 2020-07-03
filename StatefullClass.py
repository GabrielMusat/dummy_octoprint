import typing as T


class StatefulClass:
    def __init__(self, state: dict):
        self.state = state

    def set(self, chain_props: T.List[str], value: T.Any):
        def nested(root: dict, chain: T.List[str]):
            if len(chain) == 0:
                return
            elif len(chain) == 1:
                root[chain[0]] = value
            else:
                nested(root[chain[0]], chain[1:])
        nested(self.state, chain_props)

    def get(self, chain_props: T.List[str]) -> T.Any:
        def nested(root: dict, chain: T.List[str]):
            if len(chain) == 0:
                return
            elif len(chain) == 1:
                return root[chain[0]]
            else:
                return nested(root[chain[0]], chain[1:])
        return nested(self.state, chain_props)
