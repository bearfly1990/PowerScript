package fun.bearfly.swagger.model;

public class EWord {
	private Long id;
	private String cnWord;
	private String enWord;

	public String getCnWord() {
		return cnWord;
	}

	public void setCnWord(String cnWord) {
		this.cnWord = cnWord;
	}

	public String getEnWord() {
		return enWord;
	}

	public void setEnWord(String enWord) {
		this.enWord = enWord;
	}

	public Long getId() {
		return id;
	}

	public void setId(Long id) {
		this.id = id;
	}
}
