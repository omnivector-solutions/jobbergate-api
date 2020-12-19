var vpcData = {
    public: {
        vpcId: "vpc-0fefba92e3234acb9",
        securityGroupIds: ["sg-0734d573f35d588b3"],
        subnetIds: [
            "subnet-0f77837e377c9f43e",
            "subnet-0cf24701a8e5f511b",
            "subnet-09d9016290e015cf8"
        ],
        albScheme: "internet-facing",
        auroraClusterCidrIp: "10.251.0.0/20"
    },
    internal: {
        vpcId: "vpc-0fefba92e3234acb9",
        securityGroupIds: ["sg-0734d573f35d588b3"],
        subnetIds: [
            "subnet-0404e360527928905",
            "subnet-0eef4b21da85112b0",
            "subnet-0d0a84da107738d97"
        ],
        albScheme: "internal",
        auroraClusterCidrIp: "10.251.0.0/20"
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

