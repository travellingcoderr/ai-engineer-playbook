using System.Threading.Tasks;
using Nexus.Application.DTOs;

namespace Nexus.Application.Services
{
    public interface ITransferService
    {
        Task<TransferResponse> TransferAsync(TransferRequest request);
    }
}
