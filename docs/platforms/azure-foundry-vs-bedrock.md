# Microsoft Foundry vs Amazon Bedrock

This is a practical comparison for someone deciding what to learn.

## Microsoft Foundry

Microsoft documentation shows that Foundry now covers model access, agent workflows, tracing, monitoring, evaluations, and a tool catalog that includes MCP servers. It also notes that Azure AI Foundry has been renamed Microsoft Foundry in current docs. citeturn584966search1turn584966search5turn584966search9turn584966search17turn584966search21

### Good fit when
- your company is Azure-heavy
- you already use Entra ID, App Service, Functions, and Key Vault
- you want closer alignment with enterprise identity and governance

### What to learn
- Foundry projects and models
- Agent Service concepts
- tracing and evaluations
- tool catalog concepts
- how MCP servers fit into tooling

## Amazon Bedrock

AWS documentation describes Bedrock as a managed service for foundation models and describes Bedrock Agents as a managed way to orchestrate interactions between models, data sources, software applications, and user conversations. Current docs also show broad model support. citeturn584966search6turn584966search10turn584966search14turn584966search22

### Good fit when
- your company is AWS-heavy
- you want managed model access and agent building in AWS
- your apps already live near Lambda, S3, IAM, and API Gateway

### What to learn
- model access patterns
- knowledge bases and agents
- IAM boundaries
- Lambda action groups
- observability and cost controls

## My blunt recommendation

Because you already have strong Azure and DevOps instincts, start with Microsoft Foundry first, then learn Bedrock enough to compare it intelligently.

That gives you both depth and breadth without scattering your effort.
