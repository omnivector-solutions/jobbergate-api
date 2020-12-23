var vpcData = {
    public: {
        vpcId: "vpc-9653c9ee",
        securityGroupIds: ["sg-cfac3d95"],
        subnetIds: [
            "subnet-02bc060304e2d7916",
            "subnet-0881906e33eb25bc0",
            "subnet-0a7b904695e55d8ed",
            "subnet-0d4605c10612b0cdb"
        ],
        albScheme: "internet-facing",
        auroraClusterCidrIp: "172.31.0.0/16"
    },
    internal: {
        vpcId: "vpc-9653c9ee",
        securityGroupIds: ["sg-cfac3d95"],
        subnetIds: [
            "subnet-02bc060304e2d7916",
            "subnet-0881906e33eb25bc0",
            "subnet-0a7b904695e55d8ed",
            "subnet-0d4605c10612b0cdb"
        ],
        albScheme: "internal",
        auroraClusterCidrIp: "172.31.0.0/16"
    }
};


module.exports = (serverless) => {
    switch (serverless.service.provider.stage) {
        case "prod":
            return vpcData.public;
        case "staging":
            return vpcData.public;
        case "edge":
            return vpcData.internal;
        default:
            return vpcData.internal;
    }
};

