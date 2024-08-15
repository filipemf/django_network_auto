from datetime import datetime
import time
from django.shortcuts import get_object_or_404, redirect, render, HttpResponse
import paramiko
from .models import Device, Log

def home(request):
    all_devices = Device.objects.all()
    cisco_devices = Device.objects.filter(vendor='cisco')
    arista_devices = Device.objects.filter(vendor='arista')
    juniper_devices = Device.objects.filter(vendor='juniper')
    last_event = Log.objects.all().order_by('-id')[:10]

    context = {
        'total_devices': len(all_devices),
        'cisco_devices': len(cisco_devices),
        'arista_devices': len(arista_devices),
        'juniper_devices': len(juniper_devices),
        'last_event': last_event,
    }
    return render(request, 'home.html', context)

def devices(request):
    all_devices = Device.objects.all()
    context = {
        'devices': all_devices,
    }
    return render(request, 'devices.html', context)

def configure(request):
    if request.method == "POST":
        selected_device_id = request.POST.getlist('device')
        cisco_command = request.POST['cisco_command'].splitlines()

        for x in selected_device_id:
            try:
                dev = get_object_or_404(Device, pk=x)
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=dev.ip_address, username=dev.username, password=dev.password)

                if dev.vendor.lower() == 'cisco':
                    conn = ssh_client.invoke_shell()
                    conn.send("conf t\n")
                    for command in cisco_command:
                        conn.send(command + "\n")
                        time.sleep(1)

                    conn.send("end\n")
                    output = conn.recv(65535)
                    print(output.decode())
                    ssh_client.close()
                
                log = Log(target=dev.ip_address, action='Configure', status='Success', timestamp=datetime.now(),message="No error")
                log.save()

            except Exception as e:
                log = Log(target=dev.ip_address, action='Configure', status='Failed', timestamp=datetime.now(),message=str(e))
                log.save()
                
        return redirect('home')
    else:
        devices = Device.objects.all()
        context = {
            'devices': devices,
            'mode': 'configure'
        }

        return render(request, 'config.html', context)
    
def verify_config(request):
    if request.method == "POST":
        result = []
        selected_device_id = request.POST.getlist('device')
        cisco_command = request.POST['cisco_command'].splitlines()

        for x in selected_device_id:
            try:
                dev = get_object_or_404(Device, pk=x)
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh_client.connect(hostname=dev.ip_address, username=dev.username, password=dev.password)

                if dev.vendor.lower() == 'cisco':
                    for command in cisco_command:
                        stdin, stdout, stderr = ssh_client.exec_command(command)
                        time.sleep(1)
                        result.append("Result on {}: {}".format(dev.ip_address, stdout.read().decode()))
                    ssh_client.close()

                log = Log(target=dev.ip_address, action='Verify', status='Success', timestamp=datetime.now(),message="No error")
                log.save()

            except Exception as e:
                log = Log(target=dev.ip_address, action='Verify', status='Failed', timestamp=datetime.now(),message=str(e))
                log.save()

        result = '\n'.join(result)
        return render(request, 'verify_result.html', {'result': result})
    else:
        devices = Device.objects.all()
        context = {
            'devices': devices,
            'mode': 'Verify Config'
        }

        return render(request, 'config.html', context)   
    
def log(request):
    logs = Log.objects.all()

    context = {
        'logs': logs,
    }

    return render(request, 'log.html', context)
    
