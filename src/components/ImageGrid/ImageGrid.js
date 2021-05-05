import React,{ useState, useEffect } from 'react';
import { ACCESS_TOKEN_NAME } from '../../constants/apiConstants';
import axios from 'axios'

const ImageGrid = () => {
    const [urls, setUrls] = useState([])

    useEffect(() => {
        getAllUrls();
    }, []);

    const imageDelete = (image_id,image_url) => {
        const data = {
            "image_url": image_url
        }
        axios.delete(`http://127.0.0.1:5000/api/v1/images/delete/${image_id}`,{
            headers: {
                Authorization: localStorage.getItem(ACCESS_TOKEN_NAME)
            },
            data
        },
        )
        .then(function () {
            window.location.reload()
        })
    }

    const getAllUrls = () => {
        axios.get('http://127.0.0.1:5000/api/v1/images/view', {
            headers: {
                Authorization: localStorage.getItem(ACCESS_TOKEN_NAME)
            }
        })
        .then((response)=>{
            const allUrls = response.data;
            setUrls(allUrls)
        })
    }

    


  return (
    <div className="img-grid">
        { urls && urls.map(url => (
            <div className="img-wrap" key={url.image_id}> 
                <img src={url.image_url} alt='images'/>
                <button className="btn btn-primary" onClick={function(){imageDelete(url.image_id, url.image_url)}}>Delete</button>
            </div>
        )) }
        
    </div>
  )
}

export default ImageGrid;