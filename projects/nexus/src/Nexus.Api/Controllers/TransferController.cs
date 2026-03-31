using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Nexus.Application.DTOs;
using Nexus.Application.Services;

namespace Nexus.Api.Controllers
{
    [ApiController]
    [Authorize]
    [Route("api/[controller]")]
    public class TransferController : ControllerBase
    {
        private readonly ITransferService _transferService;

        public TransferController(ITransferService transferService)
        {
            _transferService = transferService;
        }

        [HttpPost]
        public async Task<ActionResult<TransferResponse>> Transfer([FromBody] TransferRequest request)
        {
            var response = await _transferService.TransferAsync(request);
            
            if (!response.Success)
                return BadRequest(response);

            return Ok(response);
        }
    }
}
