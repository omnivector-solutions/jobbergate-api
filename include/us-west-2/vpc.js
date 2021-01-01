var vpcData = {
    vpcId: "vpc-9653c9ee",
    auroraClusterCidrIp: "172.31.0.0/16",
    public: {
        securityGroupIds: ["sg-cfac3d95"],
        subnetIds: [
            "subnet-02bc060304e2d7916",
            "subnet-0881906e33eb25bc0",
            "subnet-0a7b904695e55d8ed",
            "subnet-0d4605c10612b0cdb"
        ],
        albScheme: "internet-facing",
    },
    internal: {
        securityGroupIds: ["sg-cfac3d95"],
        subnetIds: [
            "subnet-02bc060304e2d7916",
            "subnet-0881906e33eb25bc0",
            "subnet-0a7b904695e55d8ed",
            "subnet-0d4605c10612b0cdb"
        ],
        albScheme: "internal",
    },
    alb: undefined // set below, based on the name of the stage
};


module.exports = (serverless) => {
    switch (serverless.service.provider.stage) {
        case "prod":
            vpcData.alb = vpcData.public;
            return vpcData;
        case "staging":
            vpcData.alb = vpcData.public;
            return vpcData;
        case "edge":
            vpcData.alb = vpcData.internal;
            return vpcData;
        default:
            vpcData.alb = vpcData.internal;
            return vpcData;
    }
};
