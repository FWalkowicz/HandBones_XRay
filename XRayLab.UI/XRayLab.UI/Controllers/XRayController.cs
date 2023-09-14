using Microsoft.AspNetCore.Mvc;
using System.Buffers.Text;
using XRayLab.UI.ApiWrapper;
using XRayLab.UI.DTO;

namespace XRayLab.UI.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class XRayController : ControllerBase
    {
        private XRayAPI _xRay;

        public XRayController()
        {
            _xRay = new XRayAPI();
        }

        public static byte[] ReadFully(Stream input)
        {
            using (MemoryStream ms = new MemoryStream())
            {
                input.CopyTo(ms);
                return ms.ToArray();
            }
        }

        [HttpPost]
        [Route("{action}")]
        [DisableRequestSizeLimit]
        public ActionResult ExecuteAI(ImageDataDTO data)
        {
            var base64 = data.Image.Replace("data:image/jpeg;base64,", "");
            var stream = new MemoryStream(Convert.FromBase64String(base64));

            //var byteAray = System.IO.File.ReadAllBytes(@"C:\temp\knife.jpeg");

            var result = _xRay.POST_ExecuteAI(ReadFully(stream), data.FileName.Trim());
            //=====
            var image = _xRay.GET_UniqueSessionImage(result.UniqueSessionId, "prediction");
            var imageMeta = _xRay.GET_UniqueSessionMeta(result.UniqueSessionId, "prediction");


            string base64ImageRepresentation = Convert.ToBase64String(ReadFully(image));
            var response = new ResponseClassDTO()
            {
                UniqueSessionId = result.UniqueSessionId,
                ImageBase64 = $"data:image/jpeg;base64,{base64ImageRepresentation}",
                Description = imageMeta,
                Files = result.Files.Where(s => !s.FileName.Contains("txt")).ToList()
            };

            return Ok(response);
        }


        [HttpGet]
        [Route("{action}/{sessionId}/{modelName}")]
        public ActionResult ChangeAIImage(string modelName, string sessionId)
        {
            //=====
            var image = _xRay.GET_UniqueSessionImage(sessionId, modelName);
            var imageMeta = _xRay.GET_UniqueSessionMeta(sessionId, modelName);

            string base64ImageRepresentation = Convert.ToBase64String(ReadFully(image));
            var response = new ResponseClassDTO()
            {
                UniqueSessionId = sessionId,
                ImageBase64 = $"data:image/jpeg;base64,{base64ImageRepresentation}",
                Description = imageMeta
            };


            return Ok(response);
        }
    }

}
