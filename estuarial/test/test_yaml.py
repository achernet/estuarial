import yaml
with open("test_yaml.yaml", 'r') as stream:
    obj = yaml.load(stream, Loader=yaml.CLoader)
    print obj

    
