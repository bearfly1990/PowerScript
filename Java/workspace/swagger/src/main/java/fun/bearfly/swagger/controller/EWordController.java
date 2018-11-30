package fun.bearfly.swagger.controller;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RestController;

import fun.bearfly.swagger.model.EWord;
import io.swagger.annotations.ApiImplicitParam;
import io.swagger.annotations.ApiImplicitParams;
import io.swagger.annotations.ApiOperation;

@RestController
@RequestMapping(value="/ewords")
public class EWordController {
	static Map<Long, EWord> ewordsMap = Collections.synchronizedMap(new HashMap<Long, EWord>());
	
	@ApiOperation(value="HelloWorld", notes="")
	@RequestMapping(value="helloworld", method=RequestMethod.GET)
	public String sayHello() {
		return "hello, world!";
	}

    @ApiOperation(value="GetEword", notes="")
    @RequestMapping(value={""}, method=RequestMethod.GET)
    public List<EWord> getEWordList() {
        List<EWord> ewords = new ArrayList<EWord>(ewordsMap.values());
        return ewords;
    }

    @ApiOperation(value="CreateEword", notes="Create Eword by Eword")
    @ApiImplicitParam(name = "eword", value = "user domain", required = true, dataType = "EWord")
    @RequestMapping(value="", method=RequestMethod.POST)
    public String postEWord(@RequestBody EWord eword) {
    	ewordsMap.put(eword.getId(), eword);
        return "success";
    }

    @ApiOperation(value="GetEwordDetails", notes="Get eword by id")
    @ApiImplicitParam(name = "id", value = "ewordID", required = true, dataType = "Long")
    @RequestMapping(value="/{id}", method=RequestMethod.GET)
    public EWord getEWord(@PathVariable Long id) {
        return ewordsMap.get(id);
    }

    @ApiOperation(value="UpdateEwordInfo", notes="Update eword by id")
    @ApiImplicitParams({
            @ApiImplicitParam(name = "id", value = "ewordID", required = true, dataType = "Long"),
            @ApiImplicitParam(name = "user", value = "ewordDomain", required = true, dataType = "EWord")
    })
    @RequestMapping(value="/{id}", method=RequestMethod.PUT)
    public String putEWord(@PathVariable Long id, @RequestBody EWord newUser) {
        EWord eword = ewordsMap.get(id);
        eword.setCnWord(newUser.getCnWord());
        eword.setEnWord(newUser.getEnWord());
        ewordsMap.put(id, eword);
        return "success";
    }

    @ApiOperation(value="DeleteEword", notes="Delete eword by id")
    @ApiImplicitParam(name = "id", value = "ewordID", required = true, dataType = "Long")
    @RequestMapping(value="/{id}", method=RequestMethod.DELETE)
    public String deleteEWord(@PathVariable Long id) {
        ewordsMap.remove(id);
        return "success";
    }


}
