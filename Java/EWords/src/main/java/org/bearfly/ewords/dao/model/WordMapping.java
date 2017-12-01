package org.bearfly.ewords.dao.model;

public class WordMapping {
    private Integer id;
    private String enword;
    private String cnword;
    private String example_sentence;
    private String comment;
    private Boolean known;
    public Integer getId() {
        return id;
    }
    public void setId(Integer id) {
        this.id = id;
    }
    public String getEnword() {
        return enword;
    }
    public void setEnword(String enword) {
        this.enword = enword;
    }
    public String getCnword() {
        return cnword;
    }
    public void setCnword(String cnword) {
        this.cnword = cnword;
    }
    public String getExample_sentence() {
        return example_sentence;
    }
    public void setExample_sentence(String example_sentence) {
        this.example_sentence = example_sentence;
    }
    public String getComment() {
        return comment;
    }
    public void setComment(String comment) {
        this.comment = comment;
    }
    public Boolean getKnown() {
        return known;
    }
    public void setKnown(Boolean known) {
        this.known = known;
    }
    public Integer getFamiliarity() {
        return familiarity;
    }
    public void setFamiliarity(Integer familiarity) {
        this.familiarity = familiarity;
    }
    private Integer familiarity;
}
