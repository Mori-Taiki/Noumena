
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

            return CreatedAtAction(nameof(GetCharacterById), new { id = character.Id }, character);
        }

        [HttpGet("{id}")]
        public async Task<IActionResult> GetCharacterById(string id)
        {
            var character = await _characterRepository.GetCharacterByIdAsync(id);

            if (character == null)
            {
                return NotFound();
            }

            return Ok(character);
        }
    }
}
