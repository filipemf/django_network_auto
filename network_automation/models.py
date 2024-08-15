from django.db import models

class Device(models.Model):
    hostname = models.CharField(max_length=255)
    ip_address = models.CharField(max_length=255)
    username = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    ssh_port = models.IntegerField(default=22)


    VENDOR_CHOICES = (
        ('cisco', 'Cisco'),
        ('arista', 'Arista'),
        ('juniper', 'Juniper'),
    )

    vendor = models.CharField(max_length=255, choices=VENDOR_CHOICES)



    def __str__(self):
        return "{}. {}".format(self.id, self.ip_address)
    

class Log(models.Model):
    target = models.CharField(max_length=255)
    action = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    timestamp = models.DateTimeField(null=True)
    message = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return "{} - {} - {}".format(self.target, self.action, self.status)
