from rest_framework import serializers

from .models import Machine


class MachineSerializer(serializers.HyperlinkedModelSerializer):
    location = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Machine
        fields = ['url', 'FQDN', 'date', 'OS', 'is_active', 'form',
                  'bios', 'prod', 'vendor', 'kernel', 'CPU', 'cores',
                  'arch', 'mem_mb', 'location']
