import React,{ useState } from 'react';
import { withRouter } from 'react-router-dom';
import { ACCESS_TOKEN_NAME } from '../../constants/apiConstants';
import axios from 'axios'

const Home = () => {
    const [file, setFile] = useState(null)
    const [error, setError] = useState(null)
    const types = ['image/png','image/jpeg']
    
    const changeHandler = (e) => {
        let selected = e.target.files[0];
        const formData = new FormData();
        
        if (selected && types.includes(selected.type)) {
            formData.append("file", selected);
            setFile(selected);
            setError('')
            axios.post('http://127.0.0.1:5000/api/v1/images/upload', formData, {
                headers: {
                    Authorization: localStorage.getItem(ACCESS_TOKEN_NAME)
                }
            })
                .then(function () {
                    window.location.reload()
                })
        } else {
            setFile(null);
            setError('Please select an image file (png or jpeg)');
        }
    }
    return(
        <div className="mt-2">
          Welcome Shopify! Click the button below to add images to the repository!
          <form>
              <label class="test">
                <input type="file" onChange={changeHandler} name='item_image_file'/>
                <span>+</span>
              </label>
            <div className="output">
                { error && <div className="error"> { error } </div>}
                { file && <div>{ file.name }</div> }
            </div>
        </form>

        </div> 
    )
}

export default withRouter(Home);