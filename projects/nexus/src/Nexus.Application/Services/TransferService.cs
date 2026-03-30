using System;
using System.Threading;
using System.Threading.Tasks;
using System.Transactions;
using Nexus.Application.DTOs;
using Nexus.Domain.Repositories;
using Nexus.Domain.ValueObjects;
using Polly;
using Polly.Registry;

namespace Nexus.Application.Services
{
    public class TransferService : ITransferService
    {
        private readonly IAccountRepository _accountRepository;
        private readonly ResiliencePipeline _resiliencePipeline;

        // Dependency Injection: Both Repository and Resilience Pipeline are injected (SOLID - D)
        public TransferService(
            IAccountRepository accountRepository, 
            ResiliencePipelineProvider<string> pipelineProvider)
        {
            _accountRepository = accountRepository;
            // Get the "default" pipeline configured in Infrastructure
            _resiliencePipeline = pipelineProvider.GetPipeline("default");
        }

        public async Task<TransferResponse> TransferAsync(TransferRequest request)
        {
            // Resilience: Execute the entire transaction inside the resilience pipeline (Retry + Timeout)
            return await _resiliencePipeline.ExecuteAsync(async ct =>
            {
                using (var scope = new TransactionScope(TransactionScopeAsyncFlowOption.Enabled))
                {
                    try
                    {
                        var fromAccount = await _accountRepository.GetByAccountNumberAsync(request.FromAccountNumber);
                        var toAccount = await _accountRepository.GetByAccountNumberAsync(request.ToAccountNumber);

                        if (fromAccount == null || toAccount == null)
                            return new TransferResponse(false, "One or both accounts not found.");

                        var amount = new Money(request.Amount, request.Currency);

                        // Domain Logic: Entities encapsulate their own rules (DDD)
                        fromAccount.Debit(amount);
                        toAccount.Credit(amount);

                        await _accountRepository.UpdateAsync(fromAccount);
                        await _accountRepository.UpdateAsync(toAccount);

                        // Complete the transaction
                        scope.Complete();

                        return new TransferResponse(true, "Transfer completed successfully", Guid.NewGuid());
                    }
                    catch (Exception)
                    {
                        // Rollback happens automatically if scope.Complete() is not called
                        // The resilience pipeline will decide if this exception warrants a retry
                        throw; 
                    }
                }
            }, CancellationToken.None);
        }
    }
}
