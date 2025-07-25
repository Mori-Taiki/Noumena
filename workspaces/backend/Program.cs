using Microsoft.AspNetCore.Builder;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Identity.Web;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using backend.Repositories;

namespace backend;

public class Program
{
    private static readonly string MyAllowSpecificOrigins = "_myAllowSpecificOrigins";
    private const string AzureAdB2CSectionName = "AzureAdB2C";

    public static void Main(string[] args)
    {
        var builder = WebApplication.CreateBuilder(args);

        var allowedOrigins = builder.Configuration.GetSection("Cors:AllowedOrigins").Value?.Split(',') ?? Array.Empty<string>();

        builder.Services.AddCors(options =>
        {
            options.AddPolicy(name: MyAllowSpecificOrigins,
                      policy =>
                      {
                          policy.WithOrigins(allowedOrigins)
                                .AllowAnyHeader()
                                .AllowAnyMethod();
                      });
        });

        // Add services to the container.
        builder.Services.AddControllers();
        builder.Services.AddEndpointsApiExplorer();
        builder.Services.AddSwaggerGen();

        var azureAdB2CSection = builder.Configuration.GetSection(AzureAdB2CSectionName);
        var useAuthentication = azureAdB2CSection.Exists() && !string.IsNullOrEmpty(azureAdB2CSection["ClientId"]);

        if (useAuthentication)
        {
            builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
                .AddMicrosoftIdentityWebApi(azureAdB2CSection);

            builder.Services.AddAuthorization();
        }

        builder.Services.AddSingleton<ICharacterRepository, Neo4jCharacterRepository>();

        var app = builder.Build();

        // Configure the HTTP request pipeline.
        if (app.Environment.IsDevelopment())
        {
            app.UseSwagger();
            app.UseSwaggerUI();
        }

        // app.UseHttpsRedirection();

        app.UseCors(MyAllowSpecificOrigins);

        if (useAuthentication)
        {
            app.UseAuthentication();
            app.UseAuthorization();
        }

        app.MapControllers();

        app.MapGet("/api/health", () => new { status = "Ok" })
           .AllowAnonymous();

        app.Run();
    }
}