import kubernetes_api
import uuid
import cmd

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class PodManager(cmd.Cmd):
    prompt = f'{bcolors.OKGREEN}TERMINALtor > {bcolors.ENDC}'

    def do_create(self, arg):
        """Create a new pod"""
        pod_name, pod_ip = create_pod()
        print(f'Pod {pod_name} created with IP address {pod_ip}')

    def do_get_all_pods(self, arg):
        """Get all pods"""
        all_pods = get_all_pods()

        print("{:<48} | {:<15}".format('Name', 'IP'))
        print("-"*(48+15+3))

        for item in all_pods:
            print("{:<48} | {:<15}".format(item['name'], item['ip']))

    def do_delete(self, name):
        """Delete a pod"""
        if not name:
            print('Pod name is required')
            return
        delete_pod(name)
        print(f'Pod {name} deleted')

    def do_quit(self, arg):
        """Quit the application"""
        return True

def create_pod():
    pod_name = f'terminaltor-{str(uuid.uuid4())}'

    pod_ip = kubernetes_api.create_pod(pod_name)
    
    return (pod_name, pod_ip)

def delete_pod(name):
    kubernetes_api.delete_pod(name)
    pass

def get_all_pods():
    return kubernetes_api.get_all_pods()

if __name__ == '__main__':
    print("""
 _____ ______________  ________ _   _   ___   _     _             
|_   _|  ___| ___ \\  \\/  |_   _| \\ | | / _ \\ | |   | |            
  | | | |__ | |_/ / .  . | | | |  \\| |/ /_\\ \\| |   | |_ ___  _ __ 
  | | |  __||    /| |\\/| | | | | . ` ||  _  || |   | __/ _ \\| '__|
  | | | |___| |\\ \\| |  | |_| |_| |\\  || | | || |___| || (_) | |   
  \\_/ \\____/\\_| \\_\\_|  |_/\\___/\\_| \\_/\\_| |_/\\_____/\\__\\___/|_|   
    """)
    manager = PodManager()
    manager.pods = set()
    manager.cmdloop()
