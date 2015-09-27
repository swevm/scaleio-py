from scaleiopy.api.scaleio.mapping.sio_generic_object import SIO_Generic_Object


class Statistics(SIO_Generic_Object):
    """ Represents one ScaleIO cluster/installation as a class object """

    def __init__(self,
        primaryReadFromDevBwc = None,
        numOfStoragePools = None,
        protectedCapacityInKb = None,
        movingCapacityInKb = None,
        activeFwdRebuildCapacityInKb = None,
        degradedHealthyVacInKb = None,
        snapCapacityInUseOccupiedInKb = None,
        snapCapacityInUseInKb = None,
        activeMovingRebalanceJobs = None,
        totalReadBwc = None,
        maxCapacityInKb = None,
        pendingBckRebuildCapacityInKb = None,
        activeMovingOutFwdRebuildJobs = None,
        secondaryVacInKb = None,
        capacityLimitInKb = None,
        pendingFwdRebuildCapacityInKb = None,
        atRestCapacityInKb = None,
        thinCapacityInUseInKb = None,
        activeMovingInBckRebuildJobs = None,
        numOfScsiInitiators = None,
        degradedHealthyCapacityInKb = None,
        numOfUnmappedVolumes = None,
        secondaryReadFromDevBwc = None,
        numOccured = None,
        totalWeightInKb = None,
        numSeconds = None,
        failedCapacityInKb = None,
        secondaryWriteBwc = None,
        numOfVolumes = None,
        activeBckRebuildCapacityInKb = None,
        failedVacInKb = None,
        pendingMovingCapacityInKb = None,
        activeMovingInRebalanceJobs = None,
        pendingMovingInRebalanceJobs = None,
        bckRebuildReadBwc = None,
        degradedFailedVacInKb = None,
        numOfSnapshots = None,
        rebalanceCapacityInKb = None,
        fwdRebuildReadBwc = None,
        activeMovingInFwdRebuildJobs = None,
        numOfSdc = None,
        numOfVtrees = None,
        thickCapacityInUseInKb = None,
        pendingRebalanceCapacityInKb = None,
        protectedVacInKb = None,
        capacityAvailableForVolumeAllocationInKb = None,
        pendingMovingInBckRebuildJobs = None,
        pendingMovingRebalanceJobs = None,
        numOfProtectionDomains = None,
        numOfSds = None,
        capacityInUseInKb = None,
        degradedFailedCapacityInKb = None,
        bckRebuildWriteBwc = None,
        numOfThinBaseVolumes = None,
        pendingMovingOutFwdRebuildJobs = None,
        secondaryReadBwc = None,
        pendingMovingOutBckRebuildJobs = None,
        rebalanceWriteBwc = None,
        primaryReadBwc = None,
        numOfVolumesInDeletion = None,
        numOfDevices = None,
        inUseVacInKb = None,
        rebalanceReadBwc = None,
        unreachableUnusedCapacityInKb = None,
        totalWriteBwc = None,
        spareCapacityInKb = None,
        activeMovingOutBckRebuildJobs = None,
        primaryVacInKb = None,
        bckRebuildCapacityInKb = None,
        numOfThickBaseVolumes = None,
        numOfMappedToAllVolumes = None,
        activeMovingCapacityInKb = None,
        pendingMovingInFwdRebuildJobs = None,
        rmcacheSizeInKb = None,
        activeRebalanceCapacityInKb = None,
        fwdRebuildCapacityInKb = None,
        fwdRebuildWriteBwc = None,
        primaryWriteBwc = None
        ):

        self.primary_ReadFromDevBwc = primaryReadFromDevBwc
        self.num_OfStoragePools = numOfStoragePools
        self.protected_CapacityInKb = protectedCapacityInKb
        self.movingCapacityInKb = movingCapacityInKb
        self.activeFwdRebuildCapacityInKb = activeFwdRebuildCapacityInKb
        self.degradedHealthyVacInKb = degradedHealthyVacInKb
        self.snapCapacityInUseOccupiedInKb = snapCapacityInUseOccupiedInKb
        self.snapCapacityInUseInKb = snapCapacityInUseInKb
        self.activeMovingRebalanceJobs = activeMovingRebalanceJobs
        self.totalReadBwc = totalReadBwc
        self.maxCapacityInKb = maxCapacityInKb
        self.pendingBckRebuildCapacityInKb = pendingBckRebuildCapacityInKb
        self.activeMovingOutFwdRebuildJobs = activeMovingOutFwdRebuildJobs
        self.secondaryVacInKb = secondaryVacInKb
        self.capacityLimitInKb = capacityLimitInKb
        self.pendingFwdRebuildCapacityInKb = pendingFwdRebuildCapacityInKb
        self.atRestCapacityInKb = atRestCapacityInKb
        self.thinCapacityInUseInKb = thinCapacityInUseInKb
        self.activeMovingInBckRebuildJobs = activeMovingInBckRebuildJobs
        self.numOfScsiInitiators = numOfScsiInitiators
        self.degradedHealthyCapacityInKb = degradedHealthyCapacityInKb
        self.numOfUnmappedVolumes = numOfUnmappedVolumes
        self.secondaryReadFromDevBwc = secondaryReadFromDevBwc
        self.failedCapacityInKb = failedCapacityInKb
        self.secondaryWriteBwc = secondaryWriteBwc
        self.numOfVolumes = numOfVolumes
        self.activeBckRebuildCapacityInKb = activeBckRebuildCapacityInKb
        self.failedVacInKb = failedVacInKb
        self.pendingMovingCapacityInKb = pendingMovingCapacityInKb
        self.activeMovingInRebalanceJobs = activeMovingInRebalanceJobs
        self.pendingMovingInRebalanceJobs = pendingMovingInRebalanceJobs
        self.bckRebuildReadBwc = bckRebuildReadBwc
        self.degradedFailedVacInKb = degradedFailedVacInKb
        self.numOfSnapshots = numOfSnapshots
        self.rebalanceCapacityInKb, = rebalanceCapacityInKb
        self.fwdRebuildReadBwc = fwdRebuildReadBwc
        self.activeMovingInFwdRebuildJobs = activeMovingInFwdRebuildJobs
        self.numOfSdc = numOfSdc
        self.numOfVtrees = numOfVtrees
        self.thickCapacityInUseInKb = thickCapacityInUseInKb
        self.pendingRebalanceCapacityInKb = pendingRebalanceCapacityInKb
        self.protectedVacInKb = protectedVacInKb
        self.capacityAvailableForVolumeAllocationInKb = capacityAvailableForVolumeAllocationInKb
        self.pendingMovingInBckRebuildJobs = pendingMovingInBckRebuildJobs
        self.pendingMovingRebalanceJobs = pendingMovingRebalanceJobs
        self.numOfProtectionDomains = numOfProtectionDomains
        self.numOfSds = numOfSds
        self.capacityInUseInKb = capacityInUseInKb
        self.degradedFailedCapacityInKb = degradedFailedCapacityInKb
        self.bckRebuildWriteBwc = bckRebuildWriteBwc
        self.numOfThinBaseVolumes = numOfThinBaseVolumes
        self.pendingMovingOutFwdRebuildJobs = pendingMovingOutFwdRebuildJobs
        self.secondaryReadBwc = secondaryReadBwc
        self.pendingMovingOutBckRebuildJobs = pendingMovingOutBckRebuildJobs
        self.rebalanceWriteBwc = rebalanceWriteBwc
        self.primaryReadBwc = primaryReadBwc
        self.numOfVolumesInDeletion = numOfVolumesInDeletion
        self.numOfDevices = numOfDevices
        self.inUseVacInKb = inUseVacInKb
        self.rebalanceReadBwc = rebalanceReadBwc
        self.unreachableUnusedCapacityInKb = unreachableUnusedCapacityInKb
        self.totalWriteBwc = totalWriteBwc
        self.spareCapacityInKb = spareCapacityInKb
        self.activeMovingOutBckRebuildJobs = activeMovingOutBckRebuildJobs
        self.primaryVacInKb = primaryVacInKb
        self.bckRebuildCapacityInKb = bckRebuildCapacityInKb
        self.numOfThickBaseVolumes = numOfThickBaseVolumes
        self.numOfMappedToAllVolumes = numOfMappedToAllVolumes
        self.activeMovingCapacityInKb = activeMovingCapacityInKb
        self.pendingMovingInFwdRebuildJobs = pendingMovingInFwdRebuildJobs
        self.rmcacheSizeInKb = rmcacheSizeInKb
        self.activeRebalanceCapacityInKb = activeRebalanceCapacityInKb
        self.fwdRebuildCapacityInKb = fwdRebuildCapacityInKb
        self.fwdRebuildWriteBwc = fwdRebuildWriteBwc
        self.primaryWriteBwc = primaryWriteBwc


    @staticmethod
    def from_dict(dict):
        """
        A convenience method that directly creates a new instance from a passed dictionary (that probably came from a
        JSON response from the server.
        """
        return Statistics(**dict)
