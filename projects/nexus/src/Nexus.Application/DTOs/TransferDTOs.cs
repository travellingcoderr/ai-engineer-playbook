using System;

namespace Nexus.Application.DTOs
{
    public record TransferRequest(
        string FromAccountNumber,
        string ToAccountNumber,
        decimal Amount,
        string Currency
    );

    public record TransferResponse(
        bool Success,
        string Message,
        Guid? TransactionId = null
    );
}
