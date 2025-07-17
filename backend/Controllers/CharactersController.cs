
using Microsoft.AspNetCore.Mvc;
using backend.Models;
using backend.Repositories;
using System.Threading.Tasks;

namespace backend.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class CharactersController : ControllerBase
    {
        private readonly ICharacterRepository _characterRepository;

        public CharactersController(ICharacterRepository characterRepository)
        {
            _characterRepository = characterRepository;
        }

        [HttpPost]
        public async Task<IActionResult> CreateCharacter([FromBody] Character character)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            await _characterRepository.CreateCharacterAsync(character);

            return CreatedAtAction(nameof(CreateCharacter), new { id = character.Id }, character);
        }
    }
}
